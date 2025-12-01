import { useRoute } from "wouter";
import { useQuery } from "@tanstack/react-query";
import PostDetail from "@/components/PostDetail";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Link } from "wouter";
import { ChevronLeft, FileQuestion } from "lucide-react";
import type { Post } from "@/components/PostCard";

export default function PostDetailPage() {
  const [match, params] = useRoute("/post/:id");
  
  const { data: post, isLoading, error } = useQuery<Post>({
    queryKey: ["/api/posts", params?.id],
    queryFn: async () => {
      const response = await fetch(`/api/posts/${params?.id}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("Post not found");
        }
        throw new Error("Failed to fetch post");
      }
      return response.json();
    },
    enabled: !!params?.id,
  });

  if (!match || !params?.id) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Skeleton className="mb-6 h-10 w-32" />
        <Card>
          <CardContent className="p-6">
            <Skeleton className="mb-4 h-8 w-3/4" />
            <div className="mb-6 flex gap-4">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-4 w-32" />
            </div>
            <Skeleton className="mb-2 h-4 w-full" />
            <Skeleton className="mb-2 h-4 w-full" />
            <Skeleton className="mb-2 h-4 w-3/4" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Link href="/">
          <Button variant="ghost" className="mb-6 gap-2" data-testid="button-back-home">
            <ChevronLeft className="h-4 w-4" />
            Back to Home
          </Button>
        </Link>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12 text-center">
            <FileQuestion className="mb-4 h-12 w-12 text-muted-foreground" />
            <h3 className="mb-2 text-lg font-semibold">Post not found</h3>
            <p className="text-muted-foreground">
              The post you're looking for doesn't exist or has been removed.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return <PostDetail post={post} />;
}
